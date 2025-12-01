import System.IO
import qualified Data.Set as Set
import qualified Data.Map as Map
main = do
    inputFile <- openFile "2019/inputs/day_3_2019.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = map parse $ lines contents
    let outSet1 = generateSet Set.empty (0,0) (head inputLines)
    let outSet2 = generateSet Set.empty (0,0) (last inputLines)
    let outSet = Set.intersection outSet1 outSet2
    print $ Set.findMin $ Set.map manDist outSet
    let outMap1 = generateMap Map.empty (0,0) 0 (head inputLines)
    let outMap2 = generateMap Map.empty (0,0) 0 (last inputLines)
    print $ Set.findMin $ Set.map (timeDist outMap1 outMap2) outSet
    putStrLn "done!"

parse = parse' [] ""

parse' output running (x:xs)
    | x == ',' = parse' (reverse running : output) "" xs
    | otherwise = parse' output (x : running) xs
parse' output running [] = reverse $ reverse running : output

generateSet output position (x:xs) = generateSet newOut newPos xs
    where (newPos, lineSet) = generateLineSet position x
          newOut = Set.union output lineSet
generateSet output _ [] = output

generateLineSet (x,y) instruction
    | dir == 'U' = ((x,y-amount), Set.fromList $ map (x,) [y-1,y-2..y-amount])
    | dir == 'R' = ((x+amount,y), Set.fromList $ map (,y) [x+1,x+2..x+amount])
    | dir == 'D' = ((x,y+amount), Set.fromList $ map (x,) [y+1,y+2..y+amount])
    | dir == 'L' = ((x-amount,y), Set.fromList $ map (,y) [x-1,x-2..x-amount])
    where dir = head instruction
          amount :: Integer = read $ tail instruction

manDist (x,y) = abs x + abs y

generateMap output position time (x:xs) = generateMap newOut newPos newTime xs
    where (newPos, newTime, lineMap) = generateLineMap position time x
          newOut = Map.unionWith const output lineMap
generateMap output _ _ [] = output

generateLineMap (x,y) time instruction
    | dir == 'U' = ((x,y-amount), time + amount, Map.fromList $ zip (map (x,) [y-1,y-2..y-amount]) [time+1..time+amount])
    | dir == 'R' = ((x+amount,y), time + amount, Map.fromList $ zip (map (,y) [x+1,x+2..x+amount]) [time+1..time+amount])
    | dir == 'D' = ((x,y+amount), time + amount, Map.fromList $ zip (map (x,) [y+1,y+2..y+amount]) [time+1..time+amount])
    | dir == 'L' = ((x-amount,y), time + amount, Map.fromList $ zip (map (,y) [x-1,x-2..x-amount]) [time+1..time+amount])
    where dir = head instruction
          amount :: Integer = read $ tail instruction

timeDist a b c = a Map.! c + b Map.! c
