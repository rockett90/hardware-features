module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [2, 'always', [
      'library'
    ]],
    'scope-empty': [2, 'never'],
  },
};
