package list;
/**
 * Implementation of list optimized for changing size
 * 
 * @author Keith Hall
 *
 * @param <E>
 */

public class LinkedList<E> implements List<E> 
{

	Node<E> head = new Node<E>(null,null,null);	// Dummy node always at beginning, not indexed
	Node<E> tail = new Node<E>(null,null,head); // Dummy node always at end, not indexed
	
	int size = 0; 	// Size of list NOT counting head and tail
	
	private Node<E> ref;		// Reference node used in several functions
	
	public LinkedList()
	{
		head.next = tail;	// Empty list only contains head and tail
	}
	
	public void add(E value)
	{
		Node<E> temp = new Node<E>(value, tail, tail.prev);	// Create new node before tail
		
		// Fix links
		tail.prev = temp;
		temp.prev.next = temp;
		
		size++; 					// Change size
	}
	
	public void add(int ndx, E value)
	{
		if (ndx == size)			// If inserting at tail
		{
			add(value);				// Automatically adds at the end
		}
	
		setRef(ndx);				// Set reference node
		
		Node<E> temp = new Node<E>(value, ref, ref.prev);	// Create temporary node ahead of reference
		
		// Fix links
		ref.prev.next = temp;
		ref.prev = temp;
		
		size++; 					// Change size
	}
	
	public E get(int ndx) 
	{
		setRef(ndx);			// Set reference node
		
		return ref.value;		// Return value at that node
	}
	
	private void setRef(int ndx)
	{	
		ref = head; // check against index!!!
		
		// Loop until at specified index
		for (int i = 0 ; i <= ndx ; i++)
		{
			ref = ref.next;
		}
	}
	
	public E set(int ndx, E value)
	{
		setRef(ndx);			// Set reference node
		
		E result = ref.value;	// Save old variable
		
		ref.value = value;		// Change to new value
		
		return result;			// Return old value
	}
	
	public E remove(int ndx)
	{
		setRef(ndx);				// Set reference node
		
		// Fix links
		ref.next.prev = ref.prev;
		ref.prev.next = ref.next;
		
		size--;						// Change size
		
		return ref.value;			// Return old value removed
	}
	
	public void clear()
	{
		// Reset head and tail links
		head.next = tail; 			
		tail.prev = head;
		
		size = 0;		// Reset Size
		
		ref = null; 	// Clear reference node to clear rest of list from memory
	}
	
	public int size()
	{
		return size;
	}
	
	public boolean isEmpty()
	{
		if (size == 0)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
	
	// STUB
	public int indexOf(E value)
	{
		return 0;
	}
	
	// STUB
	public boolean contains (E value)
	{
		return false;
	}
	
	// STUB
	public String toString( )
	{
		return "0";
	}
	
	// STUB
	public boolean equals(Object other)
	{
		return false;
	}
}
