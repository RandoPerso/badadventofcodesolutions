import System.IO
import qualified Data.Map as Map
import Data.Maybe

main = do
    inputFile <- openFile "2018/inputs/day_12_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let initialState = parseState $ words (head inputLines) !! 2
    let initialMinimum = minimum $ Map.keys initialState
    let initialMaximum = maximum $ Map.keys initialState
    let filteredTransformations = filter (\x -> last x == '#') (drop 2 inputLines)
    let validTransformations = map parseTransformation filteredTransformations
    let nextIteration = nextIteration' validTransformations
    --  putStrLn $ showState (initialState, initialMinimum, initialMaximum)
    let (final, _, _) = foldr (\_ state -> nextIteration state) (initialState, initialMinimum, initialMaximum) [1..20]
    print $ sum $ Map.keys final
    {-
    let (final2, _, _) = foldl' (\state _ -> nextIteration state) (initialState, initialMinimum, initialMaximum) [1..500]
    print $ sum' $ Map.keys final2
    -}
    let results = drop 999 $ map (\(a, _, _) -> sum $ Map.keys a) $ scanl (\state _ -> nextIteration state) (initialState, initialMinimum, initialMaximum) [1..1000]
    print ((50000000000 - 1000) * (last results - head results) + last results)
    putStrLn "done!"

parseState line = foldr (\x y -> if snd x == '#' then Map.insert (fst x) 0 y else y) Map.empty $ zip [0..length line] line

parseTransformation line = map ('#' ==) pattern
    where pattern = take 5 line

nextIteration' transformations (state, currentMinimum, currentMaximum) = (foldr (\x y -> if snd x then Map.insert (fst x) 0 y else y) Map.empty nextList, nextMin, nextMax)
    where nextList = map (\x -> (x, [Map.member a state | a <- [x-2..x+2]] `elem` transformations)) [currentMinimum-2..currentMaximum+2]
          nextMin = fst $ head $ filter snd nextList
          nextMax = fst $ last $ filter snd nextList

showState (state, currentMinimum, currentMaximum) = [if Map.member a state then '#' else '.' | a <- [currentMinimum..currentMaximum]]

foldl' f z []     =  z
foldl' f z (x:xs) =  (foldl' f $! f z x) xs



sum' = foldl' (+) 0
