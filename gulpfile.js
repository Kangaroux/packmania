const Gulp = require("gulp");
const Autoprefixer = require("gulp-autoprefixer");
const Sass = require("gulp-sass");


const src = "app/static/";
const dst = "build/";
const paths = {
  css: {
    src: src + "css/style.scss",
    dst: dst
  },

  fonts: {
    src: src + "fonts/**/*.@(woff|woff2|eot|ttf|otf)",
    dst: dst + "fonts/"
  },

  images: {
    src: src + "img/**/*.@(png|jpg|svg|gif)",
    dst: dst + "img/"
  }
}


Gulp.task("images", function() {
  return Gulp.src(paths.images.src).pipe(Gulp.dest(paths.images.dst));
});

Gulp.task("images:watch", function() {
  Gulp.watch(paths.images.src, ["images"]);
});

Gulp.task("fonts", function() {
  return Gulp.src(paths.fonts.src).pipe(Gulp.dest(paths.fonts.dst));
});

Gulp.task("fonts:watch", function() {
  Gulp.watch(paths.fonts.src, ["fonts"]);
});

Gulp.task("scss", function() {
  return Gulp.src(paths.css.src)
    .pipe(Sass({
      outputStyle: "compressed",
      includePaths: [ "node_modules"],
    })
      .on("error", Sass.logError))
    .pipe(Autoprefixer({
      cascade: false,
      browsers: ["last 2 versions", "> 1%"]
    }))
    .pipe(Gulp.dest(paths.css.dst));
});

Gulp.task("scss:watch", function () {
  Gulp.watch(paths.css.src, ["scss"]);
});


Gulp.task("default", ["scss", "images", "fonts"]);
Gulp.task("watch", ["scss", "images", "fonts", "scss:watch", "images:watch", "fonts:watch"]);
