.pragma library

/*
 * Minimal GitHub Gists REST client.
 *
 * Kept as a `.pragma library` so it holds no QML context: every entry point
 * takes an explicit options object and reports back through callbacks.
 *
 * API reference: https://docs.github.com/en/rest/gists/gists
 */

const API_ROOT = "https://api.github.com";
const API_VERSION = "2022-11-28";
const USER_AGENT = "plasma-gist-widget";

/*
 * Build the endpoint for the configured mode.
 *
 * opts: { listOwnGists, username, maxGists }
 */
function gistsUrl(opts) {
    const perPage = Math.max(1, Math.min(100, opts.maxGists || 30));

    if (opts.listOwnGists) {
        return API_ROOT + "/gists?per_page=" + perPage;
    }

    if (!opts.username) {
        return "";
    }

    return API_ROOT + "/users/" + encodeURIComponent(opts.username)
        + "/gists?per_page=" + perPage;
}

/*
 * Fetch gists.
 *
 * opts:      see gistsUrl(), plus optional `token`
 * onSuccess: function(Array<gist>)  — normalised rows, see normalise()
 * onError:   function(String message)
 */
function fetchGists(opts, onSuccess, onError) {
    const url = gistsUrl(opts);

    if (!url) {
        onError(i18nFallback("Set a GitHub username in the widget settings."));
        return;
    }

    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Accept", "application/vnd.github+json");
    xhr.setRequestHeader("X-GitHub-Api-Version", API_VERSION);
    xhr.setRequestHeader("User-Agent", USER_AGENT);

    if (opts.token) {
        xhr.setRequestHeader("Authorization", "Bearer " + opts.token);
    }

    xhr.onreadystatechange = function() {
        if (xhr.readyState !== XMLHttpRequest.DONE) {
            return;
        }

        if (xhr.status === 0) {
            onError(i18nFallback("Could not reach api.github.com."));
            return;
        }

        if (xhr.status !== 200) {
            onError(errorMessage(xhr));
            return;
        }

        let payload;
        try {
            payload = JSON.parse(xhr.responseText);
        } catch (e) {
            onError(i18nFallback("Malformed response from GitHub."));
            return;
        }

        onSuccess(payload.map(normalise));
    };

    xhr.send();
}

/*
 * Fetch one gist with its file contents.
 *
 * The list endpoint omits `content`, so opening a gist always costs a second
 * request. Files over 1 MB come back with `truncated: true` and a clipped
 * body — the caller is expected to offer the web link in that case.
 *
 * onSuccess: function(gist)  — see normaliseDetail()
 */
function fetchGist(id, opts, onSuccess, onError) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", API_ROOT + "/gists/" + encodeURIComponent(id), true);
    xhr.setRequestHeader("Accept", "application/vnd.github+json");
    xhr.setRequestHeader("X-GitHub-Api-Version", API_VERSION);
    xhr.setRequestHeader("User-Agent", USER_AGENT);

    if (opts.token) {
        xhr.setRequestHeader("Authorization", "Bearer " + opts.token);
    }

    xhr.onreadystatechange = function() {
        if (xhr.readyState !== XMLHttpRequest.DONE) {
            return;
        }

        if (xhr.status === 0) {
            onError(i18nFallback("Could not reach api.github.com."));
            return;
        }

        if (xhr.status !== 200) {
            onError(errorMessage(xhr));
            return;
        }

        try {
            onSuccess(normaliseDetail(JSON.parse(xhr.responseText)));
        } catch (e) {
            onError(i18nFallback("Malformed response from GitHub."));
        }
    };

    xhr.send();
}

/*
 * Like normalise(), but keeps every file and its body. `files` becomes an
 * array so a Repeater can walk it; the API returns it keyed by filename.
 */
function normaliseDetail(gist) {
    const files = Object.keys(gist.files || {}).map(function(key) {
        const file = gist.files[key];
        return {
            filename: file.filename,
            language: file.language || "",
            size: file.size || 0,
            content: file.content || "",
            truncated: file.truncated === true,
            rawUrl: file.raw_url || ""
        };
    });

    return {
        id: gist.id,
        description: gist.description || "",
        htmlUrl: gist.html_url,
        isPublic: gist.public === true,
        files: files
    };
}

/*
 * Flatten a gist object into the fields the delegate renders.
 */
function normalise(gist) {
    const filenames = Object.keys(gist.files || {});
    const first = filenames.length > 0 ? gist.files[filenames[0]] : null;

    return {
        id: gist.id,
        description: gist.description || "",
        htmlUrl: gist.html_url,
        isPublic: gist.public === true,
        fileCount: filenames.length,
        primaryFilename: first ? first.filename : "",
        language: first && first.language ? first.language : "",
        commentCount: gist.comments || 0,
        createdAt: gist.created_at,
        updatedAt: gist.updated_at
    };
}

function errorMessage(xhr) {
    let detail = "";
    try {
        detail = JSON.parse(xhr.responseText).message || "";
    } catch (e) {
        // Fall through to the bare status code.
    }

    switch (xhr.status) {
    case 401:
        return i18nFallback("GitHub rejected the token (401).");
    case 403:
        // 403 here is nearly always the unauthenticated 60 req/hour ceiling.
        return detail.indexOf("rate limit") !== -1
            ? i18nFallback("GitHub rate limit reached. Add a token or wait.")
            : i18nFallback("GitHub refused the request (403).");
    case 404:
        return i18nFallback("No such GitHub user.");
    default:
        return detail !== ""
            ? detail
            : i18nFallback("GitHub returned HTTP ") + xhr.status;
    }
}

/*
 * i18n() is injected by the QML engine and is unavailable in a pragma library,
 * so error strings pass through here and are translated at the call site when
 * that matters. Kept as a seam rather than sprinkling raw literals.
 */
function i18nFallback(text) {
    return text;
}
