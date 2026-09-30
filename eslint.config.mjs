/*
 * Lint rules for the plain-JavaScript half of the plasmoid
 * (package/contents/code). QML files are qmllint's job — ESLint cannot parse
 * them — so the JS inside .qml still has to be reviewed by eye.
 *
 * Deliberately free of imports so it works with any ESLint 9 or 10 install, global
 * or local, without resolving @eslint/js first.
 *
 *   npx eslint .          # or: npm run lint
 */

/*
 * `.pragma library` / `.import` are Qt's extensions to the JS grammar and are
 * a syntax error everywhere else, so blank them out into comments of exactly
 * the same length before parsing. Equal length keeps every reported line and
 * column — and therefore --fix ranges — pointing at the real file.
 */
const qmlDirectives = {
    meta: {name: "qml-directives", version: "1.0.0"},
    preprocess(text) {
        return [text.replace(/^[ \t]*\.(?:pragma|import)\b.*$/gm,
                             line => "//" + line.slice(2))];
    },
    postprocess: messagesPerBlock => messagesPerBlock[0],
    supportsAutofix: true
};

export default [
    {
        files: ["package/contents/code/**/*.js"],
        processor: qmlDirectives,
        languageOptions: {
            ecmaVersion: 2021,
            sourceType: "script",
            globals: {
                // Provided by the QML engine, not by a module import.
                Qt: "readonly",
                XMLHttpRequest: "readonly",
                console: "readonly"
            }
        },
        rules: {
            "no-var": "error",
            "prefer-const": ["error", {destructuring: "all"}],
            "no-undef": "error",
            "no-unused-vars": ["warn", {vars: "local", args: "none", caughtErrors: "none"}]
        }
    }
];
