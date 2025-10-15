(define (problem agrodrone-prob)
  (:domain agrodrone)
  (:objects
    ;; locations
    base black_spot canker melanose greening healthy - location
    ;; pesticides (unique names!)
    black_spot_p canker_p melanose_p greening_p water - pesticide
  )
  (:init
    (at base)
  )
  (:goal
    (and
      (sprayed black_spot black_spot_p)
      (sprayed canker    canker_p)
      (sprayed melanose  melanose_p)
      (sprayed greening  greening_p)
      (sprayed healthy   water)
      (at base)
    )
  )
)
