module.exports = {
    testEnvironment: "jsdom",
    setupFilesAfterEnv: ["@testing-library/jest-dom/extend-expect"],
    moduleNameMapper: {
      "\\.(css|sass|scss)$": "identity-obj-proxy",
      "\\.svg": "<rootDir>/src/__mocks__/svgMock.js",
    },
    transform: {
        "^.+\\.(js|jsx)$": "babel-jest"
      }
  };
  