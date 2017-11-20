## [Homebrew Hub](https://gbhh.avivace.com)

# Games Database

JSON and Assets Database of all the game and homebrew entries. Propose here additions, improvements and fixes, every change propagates to Homebrew Hub.

## Add a game

Start by forking this repository and cloning your fork locally.

### 1. Decide the game `slug` 

Decide a *slug* for the game you are adding. It's like an username: short, no spaces, special characters or punctuation.

>If the game is called "Super Roto Land : Tales from the Dumper", a good slug would be `super-roto-land-1`.

### 2. Create the game folder and add the related files 

Add the decided game slug in the `gamesList.json` file and create a folder with the slug as name.

>E.g. `gameList.json` will now contain `"super-loto-land-1` as element, and we created a folder named `super-roto-land-1`

In the created folder, put
- The game ROM (.gb or .gbc);
- The screenshots (PNG, JPG and BMP are supported). At least 1 screenshot is required;

### 3. Add the `game.json` file 

Now, create a file called `game.json`:

```
{
    "title": "",
    "slug": "",
    "license": "",
    "developer": "",
    "repository": "",
    "platform": "",
    "typetag": "",
    "tags": [ ],
    "screenshots" : [ ],
    "rom" : ""
}
```

Fill in every property. You can take a look at existing games to make sure everything is correct. 
[This](ucity/game.json) is an example of a correct `game.json`.

`*` represents an optional field.


| Property Name | Description                                                          | Possible values                                         |
|---------------|----------------------------------------------------------------------|---------------------------------------------------------|
| title         | The complete name, including spacing.                                | String                                                  |
| slug          | A short identificative name that will be the in the URL              | String, Only letters, underscores, dashes and numbers   |
| license       | Identifier of the license under whose terms the software is released | [Identifier](https://spdx.org/licenses/) of the license |
| developer     | Name of the developer                                                | String                                                  |
| repository *  | Repository or URL where the source can be found                      | String                                                  |
| platform      | Target console                                                       | String: `GB` or `GBC`                                   |
| typetag       | The type of the software                                             | String: `game`, `homebrew` or `demo`                    |
| tags *        | A list of the categories representing the entry                      | Array of String of existing categories                  |
| screenshots   | A list of the filenames of the screenshots in the folder             | Array of String. Names only, no path                    |
| rom           | The name of the ROM in the folder                                    | String                                                  |

**Don't remove** optional values, just leave them blank.


The possible categories are: `RPG`, `Open Source`, `Adventure`, `Action`, `Puzzle`, `Platform`.


### Check your changes and create a PR

Check the existing folders to have examples of valid entries.

You're welcome to **edit**,**correct** or **improve** existing entries.
After you're finished and you're sure everything is valid (screenshot and rom names must be identical to the file names you added in the folder) you can commit your changes and propose a Pull Request.