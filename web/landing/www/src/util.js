export const umamiEvent = (eventName, eventData) => {
    if (!Object.hasOwn(window, "umami")) {
      return
    }
    window.umami.track(eventName, eventData)
  }

export const gtagEvent = (action) => {
    if (!Object.hasOwn(window, "gtag")) {
      return
    }
    // @ts-ignore
    window.gtag("event", action)
  }