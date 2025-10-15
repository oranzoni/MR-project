(define (domain agrodrone)
  (:requirements :strips :typing)
  (:types location pesticide)
  (:predicates
    (at ?l - location)
    (loaded ?p - pesticide)
    (sprayed ?l - location ?p - pesticide)
  )
  (:action load
    :parameters (?p - pesticide)
    :precondition (at base)
    :effect (loaded ?p)
  )
  (:action fly
    :parameters (?from ?to - location)
    :precondition (at ?from)
    :effect (and (at ?to) (not (at ?from)))
  )
  (:action spray
    :parameters (?l - location ?p - pesticide)
    :precondition (and (at ?l) (loaded ?p))
    :effect (sprayed ?l ?p)
  )
)
