import {Modal} from 'react-bootstrap'
export function AddCategoryModal(props)
{
    return(
        <Modal show={props.show} onHide={props.handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Add category</Modal.Title>
            </Modal.Header>
        </Modal>
    );
}