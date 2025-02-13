import System.IO
import Data.List
import Data.Function

main = do
    inputFile <- openFile "2018/inputs/day_23_2018_ex.txt" ReadMode
    contents <- hGetContents inputFile
    let bots = map parse $ lines contents
    let largest = maximumBy (compare `on` snd) bots
    print $ count (\bot -> snd largest >= man3 (fst bot) (fst largest)) bots
    putStrLn "done!"

man3 (x1, y1, z1) (x2, y2, z2) = abs (x2 - x1) + abs (y2 - y1) + abs (z2 - z1)

count = count' 0
count' n _ [] = n
count' n f (x:xs)
    | f x = count' (n + 1) f xs
    | otherwise = count' n f xs

parse x = ((xCoord, yCoord, zCoord), range)
    where [temp1, temp2, temp3, temp4] = wordsBy ',' x
          xCoord = read $ drop 5 temp1 :: Integer
          yCoord = read temp2 :: Integer
          zCoord = read $ init temp3 :: Integer
          range = read $ drop 3 temp4 :: Integer

wordsBy separator s =  case dropWhile (== separator) s of
                                "" -> []
                                s' -> w : wordsBy separator s''
                                        where (w, s'') =
                                                break (== separator) s'
