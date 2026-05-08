module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [2, 'always', [
      'library',
      'audio-buffer'
    ]],
    'scope-empty': [2, 'never'],
  },
};
