import System.IO
import Data.List
import Data.Maybe

main = do
    inputFile <- openFile "2020/inputs/day_1_2020.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines :: [Int] = map read $ lines contents
    print $ findProperPair inputLines
    print $ findProperTrio1 inputLines
    putStrLn "done!"

findProperPair (x:xs)
    | isJust pair = x * fromJust pair
    | otherwise = findProperPair xs
    where pair = find ((== 2020) . (+ x)) xs

findProperTrio1 (x:xs)
    | isJust trioProduct = fromJust trioProduct
    | otherwise = findProperTrio1 xs
    where trioProduct = findProperTrio2 x (head xs) (tail xs)

findProperTrio2 x y xs
    | null xs = Nothing
    | isJust trio = Just $ x * y * (2020 - x - y)
    | otherwise = findProperTrio2 x (head xs) (tail xs)
    where trio = find (== (2020 - x - y)) xs
