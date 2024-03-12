import React, { useState } from "react";
import '../../global.css';
import Slider from 'react-slider';

const MIN = 0;
const MAX = 100;

export default function PriceRange({ values, setValues}) {
    return (
        <div className="priceRange">
            <div className="box">
                <h3>Price <span>Range</span></h3>
                <div className={"values"}>€{values[0]} - €{values[1]}</div>
                <small>
                    Current range: €{values[1] - values[0]}
                </small>

                <Slider className={"slider"}
                    onChange={setValues}
                    value={values}
                    min={MIN}
                    max={MAX} />
            </div>
        </div>
    );
}