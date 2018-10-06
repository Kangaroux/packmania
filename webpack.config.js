const Path = require("path");
const VueLoaderPlugin = require('vue-loader/lib/plugin')


module.exports = {
  entry: {
    "app": "./app/static/js/app"
  },
  output: {
    path: Path.resolve(__dirname, "build"),
    filename: "[name].js"
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: "babel-loader"
      },
      {
        test: /\.vue$/,
        loader: "vue-loader"
      }
    ]
  },
  resolve: {
    alias: {
      "vue$": "vue/dist/vue.esm.js",
      "~": Path.resolve(__dirname, "app", "static", "js"),
    },
    extensions: [".js", ".vue"]
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: "vendor",
          chunks: "all"
        }
      }
    }
  },
  plugins: [
    new VueLoaderPlugin()
  ]
};