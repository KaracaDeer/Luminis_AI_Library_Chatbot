import { useRef } from 'react'
import { gsap } from 'gsap'

export const useGSAP = () => {
  const elementRef = useRef<HTMLElement | null>(null)

  const animateIn = (delay = 0) => {
    if (elementRef.current) {
      gsap.fromTo(
        elementRef.current,
        {
          opacity: 0,
          y: 50,
          scale: 0.9,
        },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.8,
          delay,
          ease: "back.out(1.7)",
        }
      )
    }
  }

  const animateOut = () => {
    if (elementRef.current) {
      gsap.to(elementRef.current, {
        opacity: 0,
        y: -50,
        scale: 0.9,
        duration: 0.5,
        ease: "power2.inOut",
      })
    }
  }

  const hoverAnimation = () => {
    if (elementRef.current) {
      gsap.to(elementRef.current, {
        scale: 1.05,
        duration: 0.3,
        ease: "power2.out",
      })
    }
  }

  const leaveAnimation = () => {
    if (elementRef.current) {
      gsap.to(elementRef.current, {
        scale: 1,
        duration: 0.3,
        ease: "power2.out",
      })
    }
  }

  const floatingAnimation = () => {
    if (elementRef.current) {
      gsap.to(elementRef.current, {
        y: -10,
        duration: 2,
        ease: "power1.inOut",
        yoyo: true,
        repeat: -1,
      })
    }
  }

  const pulseAnimation = () => {
    if (elementRef.current) {
      gsap.to(elementRef.current, {
        scale: 1.1,
        duration: 1,
        ease: "power2.inOut",
        yoyo: true,
        repeat: -1,
      })
    }
  }

  const staggerAnimation = (elements: string, stagger = 0.1) => {
    gsap.fromTo(
      elements,
      {
        opacity: 0,
        y: 30,
      },
      {
        opacity: 1,
        y: 0,
        duration: 0.6,
        stagger,
        ease: "back.out(1.7)",
      }
    )
  }

  return {
    elementRef,
    animateIn,
    animateOut,
    hoverAnimation,
    leaveAnimation,
    floatingAnimation,
    pulseAnimation,
    staggerAnimation,
  }
}
