import System.IO
import qualified Data.Set as Set
import qualified Data.List as List
import qualified Data.Map as Map
import Data.Maybe

main = do
    inputFile <- openFile "2025/inputs/day_8_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = map parse $ lines contents
    let inputSet = Set.fromList $ map Set.singleton inputLines
    let inputMap = makeConnectionsMap Map.empty inputLines
    let inputList = List.sort $ Map.keys inputMap
    print $ doIt inputSet inputMap inputList 1000
    print $ doIt2 inputSet inputMap inputList
    putStrLn "done!"

doIt groups _ _ 0 = doProd $ reverse $ List.sort $ map Set.size $ Set.toList groups
doIt groups inputMap (q:xs) counter
    | y `Set.member` group = doIt groups inputMap xs (counter - 1)
    | otherwise = doIt newGroups inputMap xs (counter - 1)
    where (x, y) = fromJust $ Map.lookup q inputMap
          group = head $ Set.toList $ Set.filter (Set.member x) groups
          otherGroup = head $ Set.toList $ Set.filter (Set.member y) groups
          newGroups = Set.insert (Set.union group otherGroup) $ Set.delete group $ Set.delete otherGroup groups

doIt2 groups inputMap (q:xs)
    | y `Set.member` group = doIt2 groups inputMap xs
    | Set.size newGroups == 1 = fst3 x * fst3 y
    | otherwise = doIt2 newGroups inputMap xs
    where (x, y) = fromJust $ Map.lookup q inputMap
          group = head $ Set.toList $ Set.filter (Set.member x) groups
          otherGroup = head $ Set.toList $ Set.filter (Set.member y) groups
          newGroups = Set.insert (Set.union group otherGroup) $ Set.delete group $ Set.delete otherGroup groups

fst3 (a,_,_) = a

{-
doIt groups things (x:xs)
    | closest `Set.member` group = doIt groups things xs
    | otherwise = doIt newGroups things xs
    where closest = getClosest 99999999999999999999999999999999 (0, 0, 0) x things
          group = head $ Set.toList $ Set.filter (Set.member x) groups
          otherGroup = head $ Set.toList $ Set.filter (Set.member closest) groups
          newGroups = Set.insert (Set.union group otherGroup) $ Set.delete group $ Set.delete otherGroup groups
doIt groups _ [] = doProd $ reverse $ List.sort $ Set.toList groups
-}

makeConnectionsMap output (x:xs) = makeConnectionsMap newOutput xs
    where current = Map.fromList $ map (\y -> (distSquared x y, (x, y))) xs
          newOutput = Map.union current output
makeConnectionsMap output [] = output

{-
getClosest bestDist best y (x:xs)
    | y == x = getClosest bestDist best y xs
    | distSquared y x < bestDist = getClosest (distSquared y x) x y xs
    | otherwise = getClosest bestDist best y xs
getClosest _ best _ [] = best
-}

doProd (a:b:c:xs) = a * b * c

parse = parse' [] ""

parse' output running (x:xs)
    | x == ',' = parse' (reverse running : output) "" xs
    | otherwise = parse' output (x : running) xs
parse' output running [] = parse'' $ reverse $ reverse running : output

parse'' :: [String] -> (Integer, Integer, Integer)
parse'' [a,b,c] = (read a, read b, read c)

distSquared (a,b,c) (x,y,z) = (a - x) ^ 2 + (b - y) ^ 2 + (c - z) ^ 2
