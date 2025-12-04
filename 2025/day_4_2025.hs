import System.IO
import qualified Data.Set as Set

main = do
    inputFile <- openFile "2025/inputs/day_4_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = linesToSet Set.empty $ zip [0..] $ lines contents
    print $ Set.size $ Set.filter (\x -> 4 > Set.size (Set.intersection inputLines (getNeighbors x))) inputLines
    print $ removeAll 0 inputLines
    putStrLn "done!"

linesToSet output ((y, q):xs) = linesToSet (addThings output q' y) xs
    where q' = zip [0..] q
linesToSet output [] = output

addThings output ((x, q):xs) y
    | q == '.' = addThings output xs y
    | otherwise = addThings (Set.insert (x, y) output) xs y
addThings output [] _ = output

getNeighbors (x, y) = Set.fromList [(x+1, y), (x-1, y), (x,y+1), (x,y-1), (x+1,y+1), (x+1,y-1), (x-1,y+1), (x-1,y-1)]

removeAll output input
    | Set.size q == 0 = output
    | otherwise = removeAll (output + Set.size q) (Set.difference input q)
    where q = Set.filter (\x -> 4 > Set.size (Set.intersection input (getNeighbors x))) input
