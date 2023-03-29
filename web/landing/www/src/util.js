export const umamiEvent = (eventName, eventData) => {
    if (!Object.hasOwn(window, "umami")) {
      return
    }
    window.umami.trackEvent(eventName, eventData)
  }