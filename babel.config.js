/**
 * @type {TransformOptions}
 */
export default {
  browserslistEnv: 'javascripts',
  presets: [
    [
      '@babel/preset-env',
      {
        // Apply bug fixes to avoid transforms
        bugfixes: true,

        // Apply smaller "loose" transforms for browsers
        loose: true
      }
    ]
  ],
  env: {
    test: {
      browserslistEnv: 'node'
    }
  }
}

/**
 * @import { TransformOptions } from '@babel/core'
 */
