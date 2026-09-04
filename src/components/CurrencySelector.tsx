import React, { useState, useEffect } from 'react';
import { CURRENCIES } from '../lib/currency';

export default function CurrencySelector() {
  const [currency, setCurrency] = useState('EUR');

  useEffect(() => {
    const saved = localStorage.getItem('odontoscore_currency');
    if (saved && CURRENCIES[saved]) {
      setCurrency(saved);
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newCurr = e.target.value;
    setCurrency(newCurr);
    localStorage.setItem('odontoscore_currency', newCurr);
    window.dispatchEvent(new CustomEvent('odontoscore:currency', { detail: { currency: newCurr } }));
  };

  return (
    <div className="currency-selector-wrapper">
      <select
        id="globalCurrencySelect"
        className="currency-select"
        aria-label="Seleccionar País y Moneda"
        value={currency}
        onChange={handleChange}
      >
        <option value="EUR">EUR (€) · España</option>
        <option value="COP">COP ($) · Colombia</option>
        <option value="MXN">MXN ($) · México</option>
        <option value="USD">USD ($) · Estados Unidos</option>
        <option value="PEN">PEN (S/.) · Perú</option>
        <option value="ARS">ARS ($) · Argentina</option>
        <option value="CLP">CLP ($) · Chile</option>
        <option value="GBP">GBP (£) · Reino Unido</option>
      </select>
    </div>
  );
}
