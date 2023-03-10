# Changelog

## 10/3-2023

- The owner of a new pokedex is no longer passed to the form via a hidden field, but is automatically input in the view.

## 9/3-2023

- Descriptions are no longer mandatory when creating PokedexEntries.


## 26/2-2023

- New list- and detailviews moves.

- New styling for type icons.

- Adjusted the size of the header buttons.

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
