# Changelog

## 28/3-2024

- Removed populating functions from migrations.

- Added management command to populate database.

- Add search fields to some models in django admin.


## 20/6-2023

- It is now possible to add moves to a pokémon from the UI.

  - It is fugly, but it works.

## 5/6-2023

- Added basic pokémon character functionality.

- Added titles to Character model.

## 5/5-2023

- Added slugs to the Character, World, Profile and Pokedex models.

## 3/5-2023

- Fixed table row height in pokédex while waiting for images to load.

- Installed Django debug toolbar

- Fixed an issue where pokedexes with owners could not be accessed.

## 12/3-2023

- Pokédex model in the admin page no longer crashes at it attempts to load all entries.

## 11/3-2023

- List- and detailview for abilities with templates.

## 10/03-2023

- Added the world and character model and basic views and templates for viewing and creation (no update views).

- The owner of a new pokedex is no longer passed to the form via a hidden field, but is automatically input in the view.

## 9/3-2023

- Descriptions are no longer mandatory when creating PokedexEntries.

## 26/2-2023

- New list- and detailviews moves.

- New styling for type icons.

- Adjusted the size of the header buttons.

- Filter options on pokedex, navigation buttons at the bottom.

## 21/2-2023

- Header navigation with burger menu for mobile users.

## 19/2-2023

- New create-, update-, and deleteviews for Pokedex objects.

- New create-, update-, detail-, and deleteviews for PokedexEntry objects.

  - The detailview for a PokedexEntry is the same as for species, but with slightly more information.

- Added "owner"-field to Pokedex.

- Added "description"-field to PokedexEntry.

  - This field will override the species' description field in the detail view.

- The pokedex overview is prettier.

- Prettier mobile UI.
