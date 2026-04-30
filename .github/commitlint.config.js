module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [2, 'always', [
      'library',
      'my-first-feature'
    ]],
    'scope-empty': [2, 'never'],
  },
};
