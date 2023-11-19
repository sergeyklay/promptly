/**
 * This file is part of the Promptly.
 *
 * Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
 *
 * For the full copyright and license information, please view
 * the LICENSE file that was distributed with this source code.
 */

const TerserPlugin = require('terser-webpack-plugin');
const path = require('path');

const rootDir = path.resolve(__dirname);
const jsSourceDir = path.join(rootDir, 'js');
const outputDir = path.join(rootDir, '..', 'promptly', 'static');
const jsOutputDir = path.join(outputDir, 'js');

const baseConfig = {
  entry: path.join(jsSourceDir, 'promptly.js'),
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',

  output: {
    filename: 'script.js',
    path: jsOutputDir,
  },

  module: {
    rules: [
      {
        test: /\.js?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
    ],
  },

  optimization: {
    minimize: false,
  },
};

const minConfig = {
    ...baseConfig,
  output: {
      ...baseConfig.output,
    filename: 'script.min.js',
  },
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()],
  },
  devtool: 'source-map',
};

module.exports = [baseConfig, minConfig];
