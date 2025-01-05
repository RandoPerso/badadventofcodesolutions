import System.IO
import Data.Char

main = do
    inputFile <- openFile "2018/inputs/day_5_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let final = fastReact contents
    print $ length final
    print $ minimum (zipWith (\x y -> length $ fastReact $ filter (\z -> toLower z /= x) y) ['a'..'z'] (replicate 26 contents))
    putStrLn "done!"

matching x y = (isLower x && toUpper x == y) || (isUpper x && toLower x == y)

fastReact x = fastReact' x []

fastReact' [] stack = stack
fastReact' (x:xs) stack
    | null stack = fastReact' xs [x]
    | matching x (head stack) = fastReact' xs (tail stack)
    | otherwise = fastReact' xs (x:stack)

{-
react x
    | reacting == -1 = x
    | otherwise = react (explodeAt x reacting)
    where reacting = search x

explodeAt x n = take n x ++ drop (n + 2) x

search x = search' x 0

search' (x:xs) index
    | null xs = -1
    | otherwise =
        if matching x (head xs) then
            index
        else
            search' xs (index + 1)
-}