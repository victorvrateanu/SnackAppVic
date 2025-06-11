import {Modal, Form, FormGroup, FormControl} from 'react-bootstrap'
import {useState} from 'react'
export function AddCategoryForm(props)
{
    const [name, setName] = useState('');
    const [color, setColor] = useState('');

    const saveCategory = async () => {
        const data = {
            name: name,
            color: color
        };

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/categories/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Error:', errorData);
                return; // Don't close the modal if the request failed
            }

            setName('');
            setColor('#000000'); // optional default
            props.handleClose()
        } catch (error) {
            console.error('Fetch error:', error);
        }
};

    return(
        <Modal show={props.show} onHide={props.handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Add category</Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <Form>
                    <FormGroup>
                        <Form.Label>Category name</Form.Label>
                        <FormControl
                            placeholder='Enter a category name'
                            value={name}
                            onChange={(event) => {
                                setName(event.target.value)
                            }}
                        />
                    </FormGroup>
                    <FormGroup>
                        <Form.Label>Category Color</Form.Label>
                        <FormControl
                            type='color'
                            value={color}
                            onChange={(event) => {
                                setColor((event.target.value))
                            }}
                        />
                    </FormGroup>

                    <button type="button" onClick={saveCategory}>
                        Add Category
                    </button>
                </Form>
            </Modal.Body>
        </Modal>
    );
}