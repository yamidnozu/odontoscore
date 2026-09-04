export interface CurrencyConfig {
  symbol: string;
  name: string;
  position: 'before' | 'after';
  decimals: number;
  flag: string;
  rate: number;
}

export const CURRENCIES: Record<string, CurrencyConfig> = {
  EUR: { symbol: "€", name: "Euros (EUR)", position: "after", decimals: 2, flag: "EUR", rate: 1.0 },
  COP: { symbol: "$", name: "Pesos Colombianos (COP)", position: "before", decimals: 0, flag: "COP", rate: 4350.0 },
  MXN: { symbol: "$", name: "Pesos Mexicanos (MXN)", position: "before", decimals: 2, flag: "MXN", rate: 18.8 },
  USD: { symbol: "$", name: "Dólares USA (USD)", position: "before", decimals: 2, flag: "USD", rate: 1.09 },
  PEN: { symbol: "S/.", name: "Soles Peruanos (PEN)", position: "before", decimals: 2, flag: "PEN", rate: 4.05 },
  ARS: { symbol: "$", name: "Pesos Argentinos (ARS)", position: "before", decimals: 0, flag: "ARS", rate: 1050.0 },
  CLP: { symbol: "$", name: "Pesos Chilenos (CLP)", position: "before", decimals: 0, flag: "CLP", rate: 1020.0 },
  GBP: { symbol: "£", name: "Libras Esterlinas (GBP)", position: "before", decimals: 2, flag: "GBP", rate: 0.86 }
};

export function formatPrice(amountEur: number, currencyCode: string = "EUR"): string {
  const conf = CURRENCIES[currencyCode] || CURRENCIES.EUR;
  const converted = amountEur * conf.rate;
  const numStr = conf.decimals === 0 
    ? Math.round(converted).toLocaleString("es-ES")
    : converted.toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  
  return conf.position === "after" ? `${numStr} ${conf.symbol}` : `${conf.symbol}${numStr}`;
}
