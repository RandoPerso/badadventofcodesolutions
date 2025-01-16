import System.IO
import qualified Data.Map as Map
import Data.List
import Data.Maybe

main = do
    inputFile <- openFile "2018/inputs/day_15_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let height = length inputLines
    let width = length $ head inputLines
    let terrainMap = makeMapOf inputLines '#'
    let goblinMap = makeMapOf inputLines 'G'
    let elfMap = makeMapOf inputLines 'E'
    let displayScene = (unlines .) . mapsToList height width terrainMap
    let (finalGoblins, finalElves, timer) = iterateUntilDeath terrainMap 0 (goblinMap, elfMap)
    let remainingUnits = if Map.null finalElves then finalGoblins else finalElves
    print $ timer * sum (map fst $ Map.elems remainingUnits)
    putStrLn "This will take a bit..."
    print $ fromJust $ fromJust $ find isJust $ map (\elfAttack -> iterateUntilGood terrainMap 0 (goblinMap, Map.map (\(a, b) -> (a, elfAttack)) elfMap)) [4..]
    putStrLn "done!"

makeMapOf lines searching = Map.fromList $ do
    (y, line) <- zip [0..] lines
    (x, char) <- zip [0..] line
    [((x, y), (200, 3)) | char == searching]

iterateUntilDeath terrainMap timer (goblinMap, elfMap)
    | stopping = (nextGoblin, nextElf, timer)
    | otherwise = iterateUntilDeath terrainMap (timer + 1) (nextGoblin, nextElf)
    where (nextGoblin, nextElf, stopping) = nextIteration terrainMap (goblinMap, elfMap)

iterateUntilGood terrainMap timer (goblinMap, elfMap)
    | Map.size elfMap > Map.size nextElf = Nothing
    | stopping = Just $ timer * sum (map fst $ Map.elems nextElf)
    | otherwise = iterateUntilGood terrainMap (timer + 1) (nextGoblin, nextElf)
    where (nextGoblin, nextElf, stopping) = nextIteration terrainMap (goblinMap, elfMap)

nextIteration terrainMap (goblinMap, elfMap) = (newGoblins, newElves, stopping)
    where moveOrder = sortBy (\(a, _) (b, _) -> getReadingOrder a b) (map (, 'E') (Map.keys elfMap) ++ map (, 'G') (Map.keys goblinMap))
          (newGoblins, newElves, _, stopping) = foldl (decideLogic terrainMap) (goblinMap, elfMap, Map.empty, False) moveOrder

decideLogic terrainMap (goblinMap, elfMap, excludedMap, stopping) (unitLocation, unitType)
    | Map.member unitLocation excludedMap = (goblinMap, elfMap, excludedMap, stopping)
    | Map.null enemyMap = (goblinMap, elfMap, excludedMap, True)
    | isJust bestAttack = nextAttackState
    | isJust bestAttack2 = nextAttackState2
    | isJust bestMovement = nextMovementState
    | otherwise = (goblinMap, elfMap, excludedMap, False)
    where (allyMap, enemyMap) = if unitType == 'E' then (elfMap, goblinMap) else (goblinMap, elfMap)
          bestAttack = getBest $ createEnemies unitLocation enemyMap
          nextAttackState' = getNextAttackState enemyMap allyMap excludedMap unitLocation (tupAdd unitLocation $ fromJust bestAttack)
          nextAttackState = (if unitType == 'G' then swap4 else id) nextAttackState'
          bestMovement = getBest $ createMovements unitLocation allyMap enemyMap terrainMap
          nextLocation = tupAdd unitLocation (fromJust bestMovement)
          nextMovementState' = (enemyMap, move unitLocation nextLocation allyMap, excludedMap, False)
          nextMovementState = (if unitType == 'G' then swap4 else id) nextMovementState'
          bestAttack2 = if isJust bestMovement then getBest $ createEnemies nextLocation enemyMap else Nothing
          nextAttackState2'' = getNextAttackState enemyMap allyMap excludedMap unitLocation (tupAdd nextLocation $ fromJust bestAttack2)
          nextAttackState2' = adjustOnSecond (move unitLocation nextLocation) nextAttackState2''
          nextAttackState2 = (if unitType == 'G' then swap4 else id) nextAttackState2'

move key1 key2 givenMap = Map.insert key2 value $ Map.delete key1 givenMap
    where value = givenMap Map.! key1

compareMaybes a b = case (isNothing a, isNothing b) of
    (True, True) -> EQ
    (True, _) -> GT
    (_, True) -> LT
    (_, _) -> fromJust a `compare` fromJust b

createEnemies location enemyMap = map (\x -> if Map.member x enemyMap then Map.lookup x enemyMap else Nothing) $ splitOut location

createMovements location allyMap enemyMap terrainMap
    | null goals = replicate 4 Nothing
    | otherwise = map (bfsTime [goal] walls) $ splitOut location
    where walls = Map.keys allyMap ++ Map.keys terrainMap
          goals = bfsGoals [location] (nub $ concatMap splitOut (Map.keys enemyMap)) walls
          goal = minimumBy getReadingOrder goals

getBest options = best
    where zipped = zip [(0, -1), (-1, 0), (1, 0), (0, 1)] options
          best' = minimumBy (\(_, a) (_, b) -> compareMaybes a b ) zipped
          best = if isNothing $ snd best' then Nothing else Just $ fst best'

getNextAttackState enemyMap allyMap excludedMap unitLocation attackLocation
    | nextHealth <= 0 = (Map.delete attackLocation enemyMap, allyMap, Map.insert attackLocation 0 excludedMap, False)
    | otherwise = (Map.adjust (\(a, b) -> (a - attack, b)) attackLocation enemyMap, allyMap, excludedMap, False)
    where (_, attack) = allyMap Map.! unitLocation
          nextHealth = fst (enemyMap Map.! attackLocation) - attack

bfsTime :: [(Int, Int)] -> [(Int, Int)] -> (Int, Int) -> Maybe Int
bfsTime goals walls location = if location `elem` walls then Nothing else bfsTime' 0 [location] goals walls

bfsTime' timer frontier goals walls
    | null frontier = Nothing
    | any (`elem` goals) frontier = Just timer
    | otherwise = bfsTime' (timer + 1) newFrontier goals (frontier ++ walls)
    where newFrontier = nub $ concatMap (filter (not . (`elem` walls))) [splitOut location | location <- frontier]

bfsGoals frontier goals walls
    | null frontier = []
    | any (`elem` goals) frontier = goals `intersect` frontier
    | otherwise = bfsGoals newFrontier goals (frontier ++ walls)
    where newFrontier = nub $ concatMap (filter (not . (`elem` walls))) [splitOut location | location <- frontier]

tupAdd (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)

splitOut (x, y) = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]

swap4 (a, b, c, d) = (b, a, c, d)

adjustOnSecond f (a, b, c, d) = (a, f b, c, d)

mapsToList height width terrainMap goblinMap elfMap = [[case map (Map.member (x, y)) [terrainMap, goblinMap, elfMap] of
    [True, _, _] -> '#'
    [_, True, _] -> 'G'
    [_, _, True] -> 'E'
    [_, _, _]    -> '.'
     | x <- [0..width - 1]] | y <- [0..height - 1]]

getReadingOrder (x1, y1) (x2, y2)
    | y1 /= y2 = compare y1 y2
    | otherwise = compare x1 x2