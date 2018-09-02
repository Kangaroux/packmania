const Gulp = require("gulp");
const Autoprefixer = require("gulp-autoprefixer");
const Sass = require("gulp-sass");


function buildStylesheets(prod) {
  return Gulp.src("./assets/css/*.scss")
    .pipe(Sass(prod ? { outputStyle: "compressed" } : null)
      .on("error", Sass.logError))
    .pipe(Autoprefixer({
      cascade: false,
      browsers: ["last 2 versions", "> 1%"]
    }))
    .pipe(Gulp.dest("dist/"));
}

Gulp.task("scss", function() {
  buildStylesheets(false);
});

Gulp.task("scss:prod", function() {
  buildStylesheets(true);
});

Gulp.task('scss:watch', function () {
  Gulp.watch("assets/css/**/*.scss", ['scss']);
});

Gulp.task("default", ["scss:prod"]);
Gulp.task("watch", ["scss", "scss:watch"]);
