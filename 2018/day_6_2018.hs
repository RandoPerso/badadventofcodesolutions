import System.IO
import Data.Foldable
import qualified Data.Map as Map

main = do
    inputFile <- openFile "2018/inputs/day_6_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let unparsedCoordinates = lines contents
    let coordinates = parse unparsedCoordinates
    let minX = minimum $ map fst coordinates
    let maxX = maximum $ map fst coordinates
    let minY = minimum $ map snd coordinates
    let maxY = maximum $ map snd coordinates
    let onBoundary = onBoundary' minX maxX minY maxY
    let addMatching = addMatching' coordinates onBoundary
    let sizes = foldr addMatching (Map.fromList [(x, 0) | x <- [0 .. (length coordinates - 1)]]) [(x, y) | x <- [minX .. maxX], y <- [minY .. maxY]]
    print (maximum $ Map.elems sizes)
    print (foldr (\x y -> if sum (map (manDist x) coordinates) < 10000 then y + 1 else y) 0 [(x, y) | x <- [minX .. maxX], y <- [minY .. maxY]])
    putStrLn "done!"

parse x = parse' x []

parse' [] coordinates = coordinates
parse' (x:xs) coordinates = parse' xs ((read $ init $ head split, read $ split !! 1):coordinates)
    where split = words x

manDist a b = abs (fst a - fst b) + abs (snd a - snd b)

findAll x element = findAll' x element [] 0

findAll' [] element locations index = locations
findAll' (x:xs) element locations index = findAll' xs element (if element == x then index:locations else locations) (index + 1)

onBoundary' minX maxX minY maxY coordinate = fst coordinate == minX || fst coordinate == maxX || snd coordinate == minY || snd coordinate == maxY

addMatching' locations onBoundary coordinate sizeMap
    | length matching == 1 =
        if onBoundary coordinate then
            Map.adjust (\_ -> -1) (head matching) sizeMap
        else
            Map.adjust (\x -> if x /= -1 then x + 1 else -1) (head matching) sizeMap
    | otherwise = sizeMap
    where distances = map (manDist coordinate) locations
          minDist = minimum distances
          matching = findAll distances minDist


