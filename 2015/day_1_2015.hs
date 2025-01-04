main = do
    putStrLn "ready!"
    input <- getLine
    print (loop input 0)
    print (loop2 input 0 0)

loop instructions total = if null instructions then total else loop (tail instructions) (total + if head instructions == '(' then 1 else -1)

loop2 instructions current total = if current < 0 then total else loop2 (tail instructions) (current + if head instructions == '(' then 1 else -1) (total + 1)