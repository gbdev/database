## [Homebrew Hub](https://gbhh.avivace.com)
# Games Database
JSON and Assets Database of all the game and homebrew entries. Propose here additions, improvements and fixes, every change propagates to Homebrew Hub.

## Structure

## Propose changes and improvements



## Add a game

Start by cloning this repository

```
git clone https://github.com/dmg01/database
```

Decide a *slug* for the game you are adding. It's like an username: short, no spaces, special characters or punctuation.
>If the game is called "Super Roto Land : Tales from the Dumper", a good slug would be `super-roto-land-1`.

Add the decided game slug in the `gamesList.json` file and create a folder and name it as the slug.

>E.g. `gameList.json` will now contain `"super-loto-land-1` as element, and we created a folder named `super-roto-land-1`

In the created folder, put
- The game ROM (.gb or .gbc);
- The screenshots (PNG, JPG and BMP are supported);
- The provided `game.json` file, filling out the properties.


Each Game is an object respecting the following structure

| Property Name | Description                                                          | Possible values                                         |
|---------------|----------------------------------------------------------------------|---------------------------------------------------------|
| title         | The complete name, including spacing.                                | String                                                  |
| permalink     | A short identificative name that will be the in the URL              | String, Only letters, underscores, dashes and numbers   |
| license       | Identifier of the license under whose terms the software is released | [Identifier](https://spdx.org/licenses/) of the license |
| developer     | GitHub username of the developer                                     | String                                                  |
| repository    | Repository or URL where the source can be found                      | String                                                  |
| platform      | Target console                                                       | String: `GB` or `GBC`                                   |
| typetag       | The type of the software                                             | String: `game`, `homebrew` or `demo`                    |
| tags          | A list of the categories representing the entry                      | Array of String, [existing categories]()                |

`*` represents an optional field.


**Don't remove** optional values, just leave them blank.

You're welcome to edit, correct or improve existing entries.

### Files

