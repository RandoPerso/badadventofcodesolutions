import System.IO

main = do
    inputFile <- openFile "2018/inputs/day_8_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputNumbers = map read $ words contents :: [Int]
    print $ generateSum inputNumbers
    print $ fst $ getNodeValue inputNumbers
    putStrLn "done!"

generateSum = addNode [] [] 0

addNode nodeStack dataStack total instructions = evaluateNode (head instructions : nodeStack) (instructions !! 1 : dataStack) total (drop 2 instructions)

decrementHead x = (head x - 1) : tail x

evaluateNode [] dataStack total instructions = total
evaluateNode nodeStack dataStack total instructions
    | head nodeStack == 0 = evaluateData (tail nodeStack) dataStack total instructions
    | otherwise = addNode (decrementHead nodeStack) dataStack total instructions

evaluateData nodeStack dataStack total instructions
    | head dataStack == 0 = evaluateNode nodeStack (tail dataStack) total instructions
    | otherwise = evaluateData nodeStack (decrementHead dataStack) (total + head instructions) (tail instructions)

getNodeValue instructions
    | numNodes == 0 = (sum $ take numMetadata $ drop 2 instructions, drop (numMetadata + 2) instructions)
    | otherwise = (foldl (\x y -> if y > numNodes || y == 0 then x else x + lowerNodes !! (y - 1)) 0 metadata, drop numMetadata $ snd resultOfLower)
    where numNodes = head instructions
          numMetadata = instructions !! 1
          resultOfLower = foldl cursedThing ([], drop 2 instructions) [1 .. numNodes]
          lowerNodes = reverse $ fst resultOfLower
          metadata = take numMetadata $ snd resultOfLower 

cursedThing (outputs, instructions) _ = (value:outputs, remainingInstructions)
    where (value, remainingInstructions) = getNodeValue instructions
