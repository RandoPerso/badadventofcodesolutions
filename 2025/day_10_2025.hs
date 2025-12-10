import System.IO
import Data.Ratio
import Data.Maybe
import Data.List (transpose, elemIndex, findIndex)

main = do
    inputFile <- openFile "2025/inputs/day_10_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = map parse $ lines contents
    print $ sum $ map testAll inputLines
    print $ sum $ map testAll2 inputLines
    putStrLn "done!"

parse x = (lights, buttons, volts)
    where y = words x
          lights = [i == '#' | i <- tail $ init $ head y]
          buttons = map (parse2 . tail . init) (tail $ init y)
          volts = (parse2 . tail . init) $ last y

parse2 :: String -> [Int]
parse2 = parse2' [] ""

parse2' output running (x:xs)
    | x == ',' = parse2' (reverse running : output) "" xs
    | otherwise = parse2' output (x : running) xs
parse2' output running [] = map read $ reverse $ reverse running : output

testAll (target, buttons, _) = minimum $ map sum $ filter (test target buttons) (binaryLists (length buttons))

test target buttons presses = not $ or $ doPresses target buttons presses

doPresses current [] [] = current
doPresses current (b:bs) (p:ps)
    | p == 1 = doPresses (doPress 0 current b) bs ps
    | otherwise = doPresses current bs ps

doPress ind cs [] = cs
doPress ind (c:cs) (b:bs)
    | ind == b = not c : doPress (ind + 1) cs bs
    | otherwise = c : doPress (ind + 1) cs (b:bs)

binaryLists 0 = [[]]
binaryLists n = [ x:xs | x <- [0,1], xs <- binaryLists (n-1) ]

nAryLists _ 0 = [[]]
nAryLists q n = [ x:xs | x <- [0..q], xs <- nAryLists q (n-1)]

rationals :: [Int] -> [Rational]
rationals = map fromIntegral

generateMatrix :: Int -> [[Int]] -> [[Rational]]
generateMatrix n = map (\b -> [if i `elem` b then 1 else 0 | i <- [0 .. n-1]])

generateAugMatrix :: [Int] -> [[Int]] -> [[Rational]]
generateAugMatrix q x = transpose $ y ++ [rationals q]
    where y = generateMatrix (length q) x

eliminate :: [Rational] -> Int -> [Rational] -> [Rational]
eliminate pivotRow pivotColi row = zipWith (-) row (map (factor *) pivotRow)
    where factor = row !! pivotColi

forwardElim :: [[Rational]] -> [[Rational]]
forwardElim [] = []
forwardElim matrix@(x:xs)
    | isNothing pivot' = matrix
    | otherwise = pivotRow : forwardElim newMatrix
    where pivot' = findPivot 0 matrix
          (pivotRowi, pivotColi) = fromJust pivot'
          pivotRow = map (/ (matrix !! pivotRowi !! pivotColi)) $ matrix !! pivotRowi
          newMatrix' = take pivotRowi matrix ++ drop (pivotRowi + 1) matrix
          newMatrix = map (eliminate pivotRow pivotColi) newMatrix'

findPivot :: Int -> [[Rational]] -> Maybe (Int, Int)
findPivot current matrix
    | current == length (head matrix) = Nothing
    | isNothing pivotRow = findPivot (current + 1) matrix
    | otherwise = Just (fromJust pivotRow, current)
    where pivotRow = findIndex (\a -> a !! current /= 0) matrix

backwardElim :: [[Rational]] -> [[Rational]]
backwardElim x = reverse $ backwardElim' $ reverse x

backwardElim' :: [[Rational]] -> [[Rational]]
backwardElim' [] = []
backwardElim' (x:xs)
    | isNothing pivot' = x : backwardElim' xs
    | otherwise = x : backwardElim' newXs
    where pivot' = elemIndex 1 x
          pivot = fromJust pivot'
          newXs = map (eliminate x pivot) xs

rref :: [[Rational]] -> [[Rational]]
rref x = backwardElim $ forwardElim x

getPivotCols :: [[Rational]] -> [Int]
getPivotCols x = [fromJust $ elemIndex 1 i | i <- x, 1 `elem` i]

convertRref :: [[Rational]] -> ([[Int] -> Rational], Int)
convertRref x = ([(\a -> (x !! (pivotRows !! i) !! const) - sum (zipWith (*) (rationals a) (map (\q -> x !! (pivotRows !! i) !! q) free))) | i <- [0..length pivots - 1]], length free)
    where pivots = getPivotCols x
          pivotRows = map (\q -> fromJust $ findIndex (\a -> a !! q /= 0) x) pivots
          free = filter (`notElem` pivots) [0..length (head x) - 2]
          const = length (head x) - 1

isWhole = (1 == ) . denominator

testAll2 (_, buttons, volts) = testAll2' (maximum volts) $ convertRref $ rref $ generateAugMatrix volts buttons
testAll2' upper (fs, free) = minimum $ mapMaybe (test2 fs) (nAryLists upper free)

test2 :: [[Int] -> Rational] -> [Int] -> Maybe Int
test2 fs q
    | not (all (\x -> isWhole x && x >= 0) outputs) = Nothing
    | otherwise = Just (sum q + fromInteger (numerator (sum outputs)))
    where outputs = map (\f -> f q) fs