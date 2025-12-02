import System.IO

main = do
    inputFile <- openFile "2025/inputs/day_2_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = parse contents
    print $ getTotal 0 inputLines
    print $ getTotal' 0 inputLines
    putStrLn "done!"

parse = parse' [] ""

parse' output running (x:xs)
    | x == ',' = parse' (reverse running : output) "" xs
    | otherwise = parse' output (x : running) xs
parse' output running [] = reverse $ reverse running : output

getTotal output (x:xs) = getTotal newOut xs
    where ids :: [Integer] = map read $ splitDash x
          newOut = output + count 0 isDupe [head ids .. last ids]
getTotal output [] = output

count output f (x:xs)
    | f x = count (output+x) f xs
    | otherwise = count output f xs
count output _ [] = output

splitDash = splitDash' [] ""

splitDash' output running (x:xs)
    | x == '-' = splitDash' (reverse running : output) "" xs
    | otherwise = splitDash' output (x : running) xs
splitDash' output running [] = reverse $ reverse running : output

isDupe y
    | odd (length x) = False
    | otherwise = take split x == drop split x
    where x = show y
          split = length x `div` 2

isDupe'' r x
    | length x `mod` r /= 0 = False
    | otherwise = isDupe' r (drop r x) (take r x)
isDupe' _ "" _ = True
isDupe' r x y
    | take r x /= y = False
    | otherwise = isDupe' r (drop r x) y

isDuper x = or [isDupe'' y z | y <- [1..length z `div` 2]]
    where z = show x

getTotal' output (x:xs) = getTotal' newOut xs
    where ids :: [Integer] = map read $ splitDash x
          newOut = output + count 0 isDuper [head ids .. last ids]
getTotal' output [] = output
