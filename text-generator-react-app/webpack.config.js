const path = require("path");
const autoprefixer = require("autoprefixer");
const HtmlWebpackPlugin = require("html-webpack-plugin");

const CSS_LOADER = {
  loader: "css-loader",
  options: { importLoaders: 1, sourceMap: true },
};

const SASS_LOADER = {
  loader: "sass-loader",
  options: { sourceMap: true },
};

const POSTCSS_LOADER = {
  loader: "postcss-loader",
  options: {
    postcssOptions: {
      plugins: [autoprefixer],
      sourceMap: true,
    },
  },
};

module.exports = {
  output: {
    path: path.join(__dirname, "/dist"),
    filename: "bundle.js",
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, "src/index.html"),
    }),
  ],
  devServer: {
    port: 8080,
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.s[ac]ss$/,
        use: ["style-loader", CSS_LOADER, POSTCSS_LOADER, SASS_LOADER],
      },
      {
        test: /\.css$/,
        use: ["style-loader", CSS_LOADER, POSTCSS_LOADER],
      },
      {
        test: /\.(png|gif|jpg|svg)$/,
        loader: "url-loader",
        options: { limit: false },
      },
    ],
  }
};
