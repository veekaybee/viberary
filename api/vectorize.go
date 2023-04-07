package api

func main() {

	err := python.Initialize()
	if err != nil {
		panic(err.Error())
	}
	defer python.Finalize()

	gensim := python.PyImport_ImportModule("gensim.models")
	if gensim == nil {
		panic("Error importing gensim.models")
	}
	defer gensim.DecRef()

	keyedVectors := gensim.GetAttrString("KeyedVectors")
	if keyedVectors == nil {
		panic("Error getting KeyedVectors attribute")
	}
	defer keyedVectors.DecRef()

	wordVectors := keyedVectors.CallMethodArgs("load_word2vec_format", python.PyString_FromString("path/to/pretrained/word2vec/file.bin"), python.PyBool_FromLong(1))
	if wordVectors == nil {
		panic("Error loading word2vec model")
	}
	defer wordVectors.DecRef()

	wordQuery := "cat"

	vector := wordVectors.CallMethodArgs("__getitem__", python.PyString_FromString(wordQuery))
	if vector == nil {
		panic("Error getting vector")
	}
	defer vector.DecRef()

}
