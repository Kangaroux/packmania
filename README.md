# Packmania
Packmania is a community-driven site for sharing and downloading songs and packs for Stepmania.

## Technologies
Packmania is built with the following technologies:
- Django
- Django Rest Framework
- Vue.js
- SASS

The frontend is a Vue SPA and the backend is an API built using DRF.

## Motivation
Stepmania lacks a proper hosting solution for songs/packs. The most popular site today is [stepmaniaonline](http://stepmaniaonline.net/), however the interface is extremely lacking. The filtering is limited to a basic text search, song metadata is not parsed, and you can't preview songs before downloading them.

[osu!](https://osu.ppy.sh/beatmapsets) has an official beatmap browser which is loved by the community and addresses every issue that SMO has.

## Feature List
The osu! beatmap browser is a good starting point, which would mean the following features:
- Listen to song preview in the browser
- Display song difficulities and other metadata (taps, holds, BPM, etc.)
- Extensive filtering (difficulty, genre, language, author, uploader, etc.)
- Sorting (popularity, time uploaded, length, etc.)
- User feedback (comments, thumb-up songs)

In addition, there are a few other features which would be helpful:
- Ability to tag songs (see: [Tagging](#tagging))
- "Follow" an uploader to be notified when they upload a new song/pack
- Create playlists (see: [Playlists](#playlists))

If Stepmania ever develops a leaderboard/ranking system this would double as a place to find those rankings.

## Tagging
Tags are additional attributes/keywords associated with songs/packs, and are meant to help users quickly find what they're looking for. The uploader could select relevant tags from a preset list.

## Playlists
Playlists are collections of songs/packs that users can put together and share with friends. Playlists are similar to packs in that they are a collection of songs, the difference being that users can freely modify them.

Some scenarios where playlists would be useful:
- Creating a playlist of songs that share some similar quality (genre, difficulty, etc.)
- Creating a playlist of your favorite songs in order to share between different devices