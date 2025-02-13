import System.IO
import qualified Data.Set as Set

main = do
    inputFile <- openFile "2020/inputs/day_3_2020.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let width = length $ head inputLines
    let height = length inputLines
    let inputSet = convertToSet inputLines
    print $ totalInside inputSet [(x, y) | y <- [0..height-1], let x = (y * 3) `mod` width]
    print (
        totalInside inputSet [(x, y) | y <- [0..height-1], let x = y `mod` width] *
        totalInside inputSet [(x, y) | y <- [0..height-1], let x = (y * 3) `mod` width] *
        totalInside inputSet [(x, y) | y <- [0..height-1], let x = (y * 5) `mod` width] *
        totalInside inputSet [(x, y) | y <- [0..height-1], let x = (y * 7) `mod` width] *
        totalInside inputSet [(x, y) | y <- [0,2..height-1], let x = (y `div` 2) `mod` width])
    putStrLn "done!"

totalInside set = foldr (\x y -> if Set.member x set then y + 1 else y) 0

foldrEnumerated f accumulator xs = foldr (\(y, line) output -> foldr (f y) output (zip [0..] line)) accumulator (zip [0..] xs)

convertToSet = foldrEnumerated (\y (x, char) currentSet -> if char == '.' then currentSet else Set.insert (x, y) currentSet) Set.empty
