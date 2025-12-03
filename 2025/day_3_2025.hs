import System.IO

main = do
    inputFile <- openFile "2025/inputs/day_3_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    print $ doIt 0 inputLines
    print $ doIt2 0 inputLines
    putStrLn "done!"

doIt output (x:xs)
    | null temp = doIt (output + 10 * maximum (init y) + q1) xs
    | otherwise = doIt (output + 10 * q1 + q2) xs
    where y :: [Integer] = map (read . (: [])) x
          q1 = maximum y
          temp = trim q1 y
          q2 = maximum temp
doIt output [] = output

trim y (x:xs)
    | x == y = xs
    | otherwise = trim y xs

doIt2 output (x:xs) = doIt2 (output + calcIt 0 12 y) xs
    where y :: [Integer] = map (read . (: [])) x
doIt2 output [] = output

calcIt output n y
    | n == 1 = 10 * output + maximum y
    | otherwise = calcIt (10 * output + q) (n - 1) (trim q y)
    where q = maximum (take (length y - n + 1) y)
