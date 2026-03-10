import js from "@eslint/js";
import stylistic from "@stylistic/eslint-plugin";
import globals from "globals";

export default [
  {
    ignores: ['node_modules']
  },
  js.configs.recommended,
  stylistic.configs['recommended'],
  {
    // Without this, console.log throws a "no-undef" error
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
  },
];
