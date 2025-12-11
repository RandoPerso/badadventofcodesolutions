import System.IO
import qualified Data.Set as Set
import qualified Data.Map as Map
import Debug.Trace

main = do
    inputFile <- openFile "2025/inputs/day_9_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = map parse $ lines contents
    -- convert shape into its edges
    let shapeLines = pairPoints inputLines
    -- find which direction it is turning
    -- positive means widdershins
    -- negative means clockwise
    let edgeVectors = map createVector shapeLines
    -- let signed = getSign $ sum $ map cross $ pairPoints edgeVectors
    -- manual override because stinky
    let signed = 1
    -- assign each vertex "concave" or "convex"
    -- this allows us to know whether to shrink the line to avoid intersection
    let concavityMap = createConcavityMap signed Map.empty (last shapeLines : shapeLines)
    let puffedEdges = map (order . puffAndAdjust signed concavityMap) shapeLines
    -- test every rectangle. if any intersect a puffed edge, it must've left the shape.
    let result = getMaxArea puffedEdges 0 inputLines
    print result
    putStrLn "done!"

{-
..............
.........#.#..
..............
..#......#....
..............
..#....#......
..............
.......#...#..
..............
-}

getMaxArea puffedEdges best (p:xs)
    | null xs = best
    | otherwise = getMaxArea puffedEdges newBest xs
    where newBest = foldl (getMaxArea' puffedEdges p) best xs

getMaxArea' puffedEdges p acc q
    | newArea <= acc = acc
    | any (uncurry isIntersect) [(x, y) | x <- getRectangle p q, y <- puffedEdges] = acc
    | otherwise = newArea
    where newArea = area p q

getRectangle p@(x1,y1) q@(x2,y2) = map order [(p,(x2,y1)),((x2,y1),q),(q,(x1,y2)),((x1,y2),p)]

isIntersect ((x1,y1),(x2,y2)) ((x3,y3),(x4,y4)) = anyInBound x1 x2 x3 x4 && anyInBound y1 y2 y3 y4

{-
isIntersect ((x1,y1),(x2,y2)) ((x3,y3),(x4,y4))
    | x1 == x2 && x3 == x4 = x1 == x3 && anyInBound y1 y2 y3 y4
    | y1 == y2 && y3 == y4 = y1 == y3 && anyInBound x1 x2 x3 x4
    | otherwise = anyInBound x1 x2 x3 x4 && anyInBound y1 y2 y3 y4
-}

anyInBound x1 x2 x3 x4 = x1 <= x4 && x3 <= x2
order ((x1,y1),(x2,y2)) = ((a1,b1),(a2,b2))
    where (a1,a2) = if x2 > x1 then (x1,x2) else (x2,x1)
          (b1,b2) = if y2 > y1 then (y1,y2) else (y2,y1)

puffAndAdjust signed concavityMap edge = adjust concavityMap edge $ puff signed edge
puff signed ((x1,y1),(x2,y2))
    | x1 == x2 = ((x1+signed*diffY,y1),(x2+signed*diffY,y2))
    | otherwise = ((x1,y1-signed*diffX),(x2,y2-signed*diffX))
    where diffY = getSign $ y2 - y1
          diffX = getSign $ x2 - x1
adjust concavityMap (a@(x1,y1),b@(x2,y2))
    | x1 == x2 = \((x1',y1'),(x2',y2')) -> ((x1',y1'+doFirst*diffY),(x2',y2'-doSecond*diffY))
    | otherwise = \((x1',y1'),(x2',y2')) -> ((x1'+doFirst*diffX,y1'),(x2'-doSecond*diffX,y2'))
    where diffY = getSign $ y2 - y1
          diffX = getSign $ x2 - x1
          doFirst = if concavityMap Map.! a then 1 else 0
          doSecond = if concavityMap Map.! b then 1 else 0
createConcavityMap signed output (edge1:edge2:xs) = createConcavityMap signed (Map.insert (snd edge1) concave output) (edge2:xs)
    where concave = signed * curry cross (createVector edge1) (createVector edge2) < 0
createConcavityMap _ output [_] = output

area (x1,y1) (x2,y2) = (1 + abs (x2 - x1)) * (1 + abs (y2 - y1))

getSign x = x `div` abs x
pairPoints x = zip x (tail x ++ [head x])
createVector ((x1,y1),(x2,y2)) = (x2-x1,y2-y1)
cross ((x1,y1),(x2,y2)) = x1*y2-x2*y1

parse = parse' [] ""

parse' output running (x:xs)
    | x == ',' = parse' (reverse running : output) "" xs
    | otherwise = parse' output (x : running) xs
parse' output running [] = parse'' $ reverse $ reverse running : output

parse'' :: [String] -> (Integer, Integer)
parse'' [a,b] = (read a, read b)
