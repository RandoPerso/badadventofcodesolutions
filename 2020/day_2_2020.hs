import System.IO

main = do
    inputFile <- openFile "2020/inputs/day_2_2020.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = map parse $ lines contents
    print $ count passing inputLines
    print $ count passing2 inputLines
    putStrLn "done!"

count pred = foldr (\a y -> if pred a then y + 1 else y) 0

passing ((a1, a2), b, c) = total >= a1 && total <= a2
    where total = count (== b) c

passing2 ((a1, a2), b, c) = (validA || validB) && not (validA && validB)
    where validA = c !! (a1 - 1) == b
          validB = c !! (a2 - 1) == b

parse x = ((a1, a2), b, c)
    where [a', b', c] = words x
          (a1', a2') = break (== '-') a'
          a1 :: Int = read a1'
          a2 :: Int = read $ tail a2'
          b = head b'
