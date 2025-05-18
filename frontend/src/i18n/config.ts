// Deliberately copied from https://phrase.com/blog/posts/localizing-react-apps-with-i18next/#the-demo-app-a-react-and-i18next-playground
import i18n from "i18next";
import HttpApi from "i18next-http-backend";
import { initReactI18next } from "react-i18next";

const DEFAULT_LANGUAGE = "en";

export const AVAILABLE_LANGUAGES = [
  { code: "en", label: "English" },
  { code: "id", label: "Bahasa Indonesia" },
];

// Get stored language from localStorage or default to "en"
const savedLanguage = localStorage.getItem("i18nextLng") || DEFAULT_LANGUAGE;

i18n
  .use(HttpApi)
  .use(initReactI18next)
  .init({
    lng: savedLanguage,
    fallbackLng: "en",
    debug: false,
    // ns: ["common", "settings"],
    // defaultNS: "common",
    interpolation: {
      escapeValue: false,
    },
    react: {
      useSuspense: true,
    },
  });

// Listen for language changes and store them
i18n.on("languageChanged", (lang) => {
  localStorage.setItem("i18nextLng", lang);
});

export default i18n;
