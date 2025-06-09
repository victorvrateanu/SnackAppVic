import React from 'react'
import {useEffect, useState} from "react";
import {Card} from "react-bootstrap";
import './HomePage.css';
import hourglass from '../assets/hourglass.svg';
import {CategoryList} from "../components/CategoryList.jsx";
import '../components/DurationBadge.css'
import {DurationBadge} from "../components/DurationBadge.jsx";

export function HomePage(){

    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        fetch(`${import.meta.env.VITE_API_URL}/recipes`)
            .then((response)=>{
                return response.json()
            })
            .then((data)=>{
                setRecipes(data)
            })
    }, []);

    return (
        <>
            <h1>My Recipes</h1>

            <div>
                Recipe count: {recipes.length}
            </div>
            <div className='recipe-grid'>
                {
                    recipes.map((recipe) =>{
                        return (
                            <Card>
                                <Card.Img src={recipe.pictures[0]} height={300} />
                                <Card.Body>
                                    <Card.Title>
                                        {recipe.name}
                                    </Card.Title>
                                    <CategoryList categories={recipe.categories}/>
                                    <DurationBadge duration={recipe.duration}/>

                                </Card.Body>
                            </Card>
                        )
                    })
                }
            </div>

        </>
    );
}