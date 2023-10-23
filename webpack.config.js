/**
 * This file is part of the Promptly.
 *
 * Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
 *
 * For the full copyright and license information, please view
 * the LICENSE file that was distributed with this source code.
 */

const path = require('path');
const mode = process.env.NODE_ENV === 'production' ? 'production' : 'development';

/** @type {import('webpack').Configuration } */
const config = {
  mode: mode, // 'production', 'development', 'none'
  entry: './promptly/static/js/promptly.js',

  output: {
    filename: mode === 'production' ? 'script.min.js' : 'script.js',
    path: path.resolve(__dirname, 'promptly/static/js'),
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
};

module.exports = config;
