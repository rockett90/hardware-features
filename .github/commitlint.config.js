module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [2, 'always', [
      'library',
      'audio-buffer',
      'simple-amplifier',
      'test-feature'
    ]],
    'scope-empty': [2, 'never'],
  },
};
