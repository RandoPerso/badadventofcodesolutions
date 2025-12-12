import System.IO
main = do
    inputFile <- openFile "2025/inputs/day_12_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let problems = map parse $ drop 30 inputLines
    let shapesList = getShapes inputLines
    print $ countProblems shapesList [] 0 problems
    putStrLn "done!"

countProblems shapesList remaining total (a@((x,y), shapes):xs)
    | area < shapesArea = countProblems shapesList remaining total xs
    | sum shapes <= fakeArea = countProblems shapesList remaining (total+1) xs
    | otherwise = countProblems shapesList (a:remaining) total xs
    where area = x * y
          shapesArea = sum $ zipWith (*) shapesList shapes
          fakeArea = (x `div` 3) * (y `div` 3)
countProblems _ remaining total [] = (remaining, total)

parse :: [Char] -> ((Int, Int), [Int])
parse x = (parse2 (init $ head y), map read (tail y))
    where y = words x

parse2 = parse2' [] ""

parse2' output running (x:xs)
    | x == 'x' = parse2' (reverse running : output) "" xs
    | otherwise = parse2' output (x : running) xs
parse2' output running [] = parse2'' $ reverse $ reverse running : output

parse2'' :: [String] -> (Int, Int)
parse2'' [a,b] = (read a, read b)

getShapes x = map parseShape $ group5 (take 30 x)

group5 [] = []
group5 x = concat (take 5 x) : group5 (drop 5 x)

parseShape q = length $ filter (=='#') q

