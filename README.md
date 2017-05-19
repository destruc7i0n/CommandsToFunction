# CommandsToFunction
An MCEdit filter to convert a command block chain into a function.

## How to use the filter
Select a 1x1x1 cube around a non-conditional repeating command block and run the filter. It'll traverse the line and create a function that you can then save.

## Notes
The filter also includes a small fix for any conditional commands you may have, which is done using an area effect cloud. **This requires a dummy objective named `SuccessCount` in the world**.

## Credits
* [MrGarretto](https://mrgarretto.com) for the code to traverse the command block line.

## License
MIT
