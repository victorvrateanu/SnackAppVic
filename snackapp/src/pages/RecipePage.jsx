import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import './RecipePage.css';
import {Form, FormControl, FormGroup, FormLabel} from "react-bootstrap";
import {CategoryList} from "../components/CategoryList.jsx";
import {DurationBadge} from "../components/DurationBadge.jsx";

export function RecipePage() {
  const { recipeId } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [servings, setServings] = useState(1);

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/recipes/${recipeId}`);
        if (response.ok) {
          const data = await response.json();
          setRecipe(data);
        } else {
          console.error('Failed to fetch recipe');
        }
      } catch (error) {
        console.error('Error fetching recipe:', error);
      }
    };

    fetchRecipe()
  }, [recipeId]);

  if (!recipe) {
    return (
      <>
        <h1>Recipe doesn't exist!</h1>
      </>
    );
  }

  return (
    <>
      <h1>{recipe.name}</h1>
      <p>Duration: <DurationBadge duration={recipe.duration}/></p>
      <CategoryList categories={recipe.categories}/>

      <Form onSubmit={(event) => event.preventDefault()}>
        <FormGroup>
          <FormLabel>Change serving size</FormLabel>
          <FormControl
              type='number'
              value={servings}
              onChange={(event) => {
            setServings(event.target.value)
          }} />
        </FormGroup>
      </Form>

      <h1>Ingredients</h1>

      {recipe.ingredients.map( (ingredient) => (
          <p> * {ingredient.quantity * servings} {ingredient.unit} {ingredient.name} </p>
      ))}

      <h1>Instructions</h1>
      <p>{recipe.instructions}</p>

      <h1>Pictures</h1>
      <section className="gallery-section">
        <div className="gallery">
          {recipe.pictures.map((picture, index) => (
            <img
              key={index}
              src={picture}
              alt={`Recipe image ${index + 1}`}
              style={{ width: '150px', height: 'auto', borderRadius: '8px' }}
            />
          ))}
        </div>
      </section>
    </>
  );
}