import System.IO

main = do
    inputFile <- openFile "2016/inputs/day_3_2016.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines :: [[Int]] = map (map read . words) $ lines contents
    print $ length $ filter isValid inputLines
    print $ length $ filter isValid $ convert [] inputLines
    putStrLn "done!"

isValid x = total - maxSide > maxSide
    where maxSide = maximum x
          total = sum x

convert output [] = output
convert output (a:b:c:xs) = convert (change a b c ++ output) xs

change [a1,a2,a3] [b1,b2,b3] [c1,c2,c3] = [[a1,b1,c1], [a2,b2,c2], [a3,b3,c3]]
